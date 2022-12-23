class LIS:
    __lis_data = ''
    __lis_result = {}
    __lis_error_message = ''
    __lis_format = {
        'H': [
            {'name': 'password', 'index': 3},
            {'name': 'name_of_transmitter', 'index': 4},
            {'name': 'name_of_receiver', 'index': 9},
            {'name': 'mode_of_processing', 'index': 11},
            {'name': 'protocol_version', 'index': 12},
            {'name': 'date', 'index': 13},
        ],
        'P': [
            {'name': 'serial_no', 'index': 1},
            {'name': 'name_of_patient', 'index': 5},
            {'name': 'sex', 'index': 8},
        ],
        'O': [
            {'name': 'serial_no', 'index': 1},
            {'name': 'sample_no', 'index': 3},
            {'name': 'assay', 'index': 4},
            {'name': 'priority', 'index': 5},
        ],
        'R': [
            {'name': 'serial_no', 'index': 1},
            {'name': 'assay_record', 'index': 2},
            {'name': 'result', 'index': 3},
            {'name': 'unit', 'index': 4},
            {'name': 'reference_range', 'index': 5},
            {'name': 'result_flag', 'index': 6},
            {'name': 'test_finish_time', 'index': 12},
        ],
        'Q': [
            {'name': 'serial_no', 'index': 1},
            {'name': 'sample_no', 'index': 2},
            {'name': 'assay_record', 'index': 4},
            {'name': 'required_info_status', 'index': 12},
        ],
    }
    __lis_identifier = ['H', 'P', 'O', 'R', 'Q']

    def __init__(self):
        pass

    def get_lis_data(self) -> str:
        return self.__lis_data
    
    def get_lis_result(self) -> object:
        return self.__lis_result
    
    def get_lis_error(self) -> str:
        return self.__lis_error_message

    def load_lis_data(self, lis) -> bool:
        # TODO: Find method to convert lis from other datatype into string
        if lis.count('\\r') > 3:
            lis = lis.replace('?', '')
            self.__lis_data = lis
            self.__lis_result = {}

            lis_segment = lis.split('\\r')
            for segment in lis_segment:
                try:
                    if segment.startswith(tuple(self.__lis_identifier)):
                        if not self.__extraction_identifier(segment[0:1], segment):
                            return False
                except Exception as e:
                    print(e)
                    self.__lis_error_message = '[CLASS]: ' + str(e)
                    return False
            return True
        else:
            print('Invalid LIS format!')
            self.__lis_error_message = '[CLASS]: Invalid LIS format!'
            return False

    def __extraction_identifier(self, identifier, segment) -> bool:
        if identifier in self.__lis_identifier: # Checking identifier match with defined LIS identifier
            segment_properties = segment.split('|') # Each segment_properties was joined with '|' sign inside segment
            segment_format = self.__lis_format[identifier]
            segment_properties_length = len(segment_properties)

            if not identifier in self.__lis_result.keys(): # Verify if identifier was exist in __lis_result
                # Due to identifier R, P, and O has serial no so we need to use list instead of object
                if identifier == 'R' or identifier == 'P' or identifier == 'O' or identifier == 'Q':
                    self.__lis_result[identifier] = []
                else:
                    self.__lis_result[identifier] = {}

            extracted_segment = {} # Extracted result was temporary stored inside extracted_segment
            # Every LIS has a standard placing and formatting
            for lis_segment_format in segment_format: # Looping through segment_format for the position and name
                if segment_properties_length > lis_segment_format['index']:
                    property = segment_properties[lis_segment_format['index']]
                    if len(property) == 0:
                        property = segment_properties[lis_segment_format['index'] -1]
                    property = property.strip()
                    if '^' in property:
                        if property.count('^') < len(property):
                            if lis_segment_format['name'] == 'assay':
                                property = property.replace('^', '')
                                property = property.split('\\')
                            else:
                                property = property.split('^')
                                if lis_segment_format['name'] == 'sample_no':
                                    if property[len(property) - 1] == 'A':
                                        property = property[0:len(property) -1]
                                        property = property[::-1]
                                for p in property:
                                    if p != '':
                                        property = p.strip()
                                        break;
                        else:
                            property = ''
                    extracted_segment[lis_segment_format['name']] = property
            # Exclude all segment that has .PNG extention inside result for result record
            if identifier == 'R' or identifier == 'P' or identifier == 'O' or identifier == 'Q':
                if 'result' in extracted_segment.keys():
                    if not extracted_segment['result'].endswith('.PNG'):
                        self.__lis_result[identifier].append(extracted_segment)
                else:
                    self.__lis_result[identifier].append(extracted_segment)
            else:
                self.__lis_result[identifier] = extracted_segment
            return True
        else:
            print('Invalid LIS identifier!')
            self.__lis_error_message = '[CLASS]: Invalid LIS identifier!'
            return False