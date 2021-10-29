# windows constants
WINDOW_HEIGHT = 500                                     
WINDOW_WIDTH = 800                                      
WINDOW_SIZE = f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}"
WINDOW_TITLE = "Geometric figures applications"         
WINDOW_TRANSPARENCY = "1"                               

# default frame padding
DEFAULT_FRAME_BACK_HEIGHT_PERCENT = 0.1                 
DEFAULT_FRAME_BACK_HEIGHT = DEFAULT_FRAME_BACK_HEIGHT_PERCENT * WINDOW_HEIGHT
DEFAULT_FRAME_DATA_HEIGHT = (1-DEFAULT_FRAME_BACK_HEIGHT_PERCENT) * WINDOW_HEIGHT

# main menu constants
MM_BUTTONS_DICT = {1 : "Continue", 2 : "New session", 3 : "Save session", 4 : "Load session", 5 : "Exit"}
MM_BUTTON_WIDTH_PERCENT = 0.05                         
MM_BUTTON_Y_PADDING_PERCENT = 0.02                   
MM_BUTTON_GRID_PADDING_PERCENT = 0.02                   
MM_BUTTON_WIDTH = int (WINDOW_WIDTH * MM_BUTTON_WIDTH_PERCENT)
MM_BUTTON_Y_PADDING = int (WINDOW_HEIGHT * MM_BUTTON_Y_PADDING_PERCENT )
MM_BUTTON_GRID_PADDING = WINDOW_HEIGHT * MM_BUTTON_GRID_PADDING_PERCENT

# new session windows constants
NS_COMBO_X_POS_PERCENT = 0.05                      
NS_COMBO_Y_POS_PERCENT = 0.05                      
NS_COMBO_X_POS = int ( WINDOW_WIDTH * NS_COMBO_X_POS_PERCENT)
NS_COMBO_Y_POS = int ( WINDOW_HEIGHT * NS_COMBO_Y_POS_PERCENT)
NS_COMBO_WIDTH_PERCENT = 0.03
NS_COMBO_WIDTH = int (NS_COMBO_WIDTH_PERCENT * WINDOW_WIDTH) 
NS_BUTTON_SELECT_X_POS_PERCENT = 0.25               
NS_BUTTON_SELECT_X_POS = int ( (NS_COMBO_X_POS_PERCENT + NS_BUTTON_SELECT_X_POS_PERCENT) *  WINDOW_WIDTH)
NS_BUTTON_SELECT_Y_POS = NS_COMBO_Y_POS 
NS_BUTTON_SELECT_WIDTH_PERCENT = 0.01               
NS_BUTTON_SELECT_WIDTH = int (NS_BUTTON_SELECT_WIDTH_PERCENT * WINDOW_WIDTH )
NS_BUTTON_SELECT_Y_PADDING_PERCENT = 0             
NS_BUTTON_Y_PADDING = int (WINDOW_HEIGHT * NS_BUTTON_SELECT_Y_PADDING_PERCENT )
NS_LABEL_PROPERTIES_X_POS_PERCENT = 0.6       
NS_LABEL_PROPERTIES_X_POS = int (NS_LABEL_PROPERTIES_X_POS_PERCENT * WINDOW_WIDTH)
NS_LABEL_PROPERTIES_Y_POS = NS_COMBO_Y_POS 
NS_AREA_LABEL_Y_POS_PERCENT = 3
NS_AREA_LABEL_Y_POS = int (NS_LABEL_PROPERTIES_Y_POS * (1 +NS_AREA_LABEL_Y_POS_PERCENT ))
NS_CIRCUM_LABEL_Y_POS_PERCENT = 0.5
NS_CIRCUM_LABEL_Y_POS = int (NS_AREA_LABEL_Y_POS * (1+NS_CIRCUM_LABEL_Y_POS_PERCENT)  )
NS_INSCR_LABEL_Y_POS = int (NS_CIRCUM_LABEL_Y_POS +  (NS_CIRCUM_LABEL_Y_POS_PERCENT)*NS_AREA_LABEL_Y_POS  )
NS_R_CIRCUM_LABEL_Y_POS = int (NS_INSCR_LABEL_Y_POS  +  (NS_CIRCUM_LABEL_Y_POS_PERCENT)*NS_AREA_LABEL_Y_POS  )
NS_ENTRY_VALUES_WIDTH_PERCENT = 0.015
NS_ENTRY_VALUES_WIDTH = int (NS_ENTRY_VALUES_WIDTH_PERCENT * WINDOW_WIDTH)
NS_ENTRY_VALUES_X_PERCENT = 0.85
NS_ENTRY_VALUES_X = int (NS_ENTRY_VALUES_X_PERCENT  * WINDOW_WIDTH )
NS_LEFT_FRAME_X_PERCENT = NS_COMBO_X_POS_PERCENT
NS_LEFT_FRAME_X = int ( WINDOW_WIDTH * NS_LEFT_FRAME_X_PERCENT)
NS_LEFT_FRAME_Y_PERCENT = 0.15
NS_LEFT_FRAME_Y = int (NS_LEFT_FRAME_Y_PERCENT * WINDOW_HEIGHT)
NS_LEFT_FRAME_WIDTH_PERCENT = 0.5
NS_LEFT_FRAME_WIDTH = int (NS_LEFT_FRAME_WIDTH_PERCENT * WINDOW_WIDTH)
NS_LEFT_FRAME_HEIGHT_PERCENT = 0.5
NS_LEFT_FRAME_HEIGHT = int (NS_LEFT_FRAME_HEIGHT_PERCENT * WINDOW_HEIGHT)
# NS_CALC_BUTTON_WIDTH_PERCENT = 0.01
# NS_CALC_BUTTON_WIDTH = int (NS_CALC_BUTTON_WIDTH_PERCENT * WINDOW_WIDTH)
NS_CALC_BUTTON_X_POS_PERCENT = 0.05
NS_CALC_BUTTON_X_POS = int (NS_COMBO_X_POS + NS_CALC_BUTTON_X_POS_PERCENT * WINDOW_WIDTH) 
NS_CALC_BUTTON_Y_POS_PERCENT = 0.35
NS_CALC_BUTTON_Y_POS = int (NS_CALC_BUTTON_Y_POS_PERCENT * DEFAULT_FRAME_DATA_HEIGHT)
NS_TRIANGLE_IMAGE_X_PERCENT = 0.25
NS_TRIANGLE_IMAGE_X = int (NS_TRIANGLE_IMAGE_X_PERCENT * WINDOW_WIDTH)
NS_TRIANGLE_IMAGE_Y_PERCENT = 0.2
NS_TRIANGLE_IMAGE_Y = int (NS_TRIANGLE_IMAGE_Y_PERCENT * WINDOW_HEIGHT)
NS_TRIANGLE_IMAGE_WIDTH_PERCENT = 0.2
NS_TRIANGLE_IMAGE_WIDTH = int (NS_TRIANGLE_IMAGE_WIDTH_PERCENT * WINDOW_WIDTH )
NS_TRIANGLE_VALUES_WIDTH_PERCENT = 0.005
NS_TRIANGLE_VALUES_WIDTH = int (NS_TRIANGLE_VALUES_WIDTH_PERCENT * WINDOW_WIDTH)
NS_TRIANGLE_A_VALUE_X_OFFSET = 15
NS_TRIANGLE_A_VALUE_X = int (NS_TRIANGLE_IMAGE_X + NS_TRIANGLE_A_VALUE_X_OFFSET)
NS_TRIANGLE_A_VALUE_Y_OFFSET = 50
NS_TRIANGLE_A_VALUE_Y = int (NS_TRIANGLE_IMAGE_Y + NS_TRIANGLE_A_VALUE_Y_OFFSET)
NS_TRIANGLE_B_VALUE_X_OFFSET = 120
NS_TRIANGLE_B_VALUE_X = int (NS_TRIANGLE_IMAGE_X + NS_TRIANGLE_B_VALUE_X_OFFSET)
NS_TRIANGLE_B_VALUE_Y_OFFSET = NS_TRIANGLE_A_VALUE_Y_OFFSET
NS_TRIANGLE_B_VALUE_Y = int (NS_TRIANGLE_IMAGE_Y + NS_TRIANGLE_B_VALUE_Y_OFFSET)
NS_TRIANGLE_C_VALUE_X_OFFSET = int (0.5 * NS_TRIANGLE_IMAGE_WIDTH - 10)
NS_TRIANGLE_C_VALUE_X = int (NS_TRIANGLE_IMAGE_X + NS_TRIANGLE_C_VALUE_X_OFFSET)
NS_TRIANGLE_C_VALUE_Y_OFFSET = 155
NS_TRIANGLE_C_VALUE_Y = int (NS_TRIANGLE_IMAGE_Y + NS_TRIANGLE_C_VALUE_Y_OFFSET)
