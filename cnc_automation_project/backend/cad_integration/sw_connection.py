import os
import platform

try:
    import win32com.client
    import pythoncom
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False

class SolidWorksConnection:
    def __init__(self):
        self.sw_app = None
        self.model = None

    def connect(self):
        """Establishes a connection to SolidWorks via COM interface."""
        if not WIN32_AVAILABLE:
            print("SolidWorks integration is only supported on Windows. Running in mock mode/disabled.")
            return False
            
        try:
            # pythoncom.CoInitialize() is required for multi-threading/web server environments
            pythoncom.CoInitialize() 
            self.sw_app = win32com.client.Dispatch("SldWorks.Application")
            self.sw_app.Visible = True
            print("Successfully connected to SolidWorks.")
            return True
        except Exception as e:
            print(f"Failed to connect to SolidWorks. Ensure it is installed. Error: {e}")
            return False

    def open_part(self, file_path):
        """Opens a specific SolidWorks part file."""
        if not self.sw_app:
            print("SolidWorks is not connected.")
            return None
        
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return None

        # 1 = swDocPART, 2 = swDocASSEMBLY, 3 = swDocDRAWING
        file_type = 1 
        options = 1 # swOpenDocOptions_Silent
        configuration = ""
        
        # OpenDoc6 parameters: (FileName, Type, Options, Configuration, &Errors, &Warnings)
        self.model = self.sw_app.OpenDoc6(file_path, file_type, options, configuration, 0, 0)
        
        if self.model:
            print(f"Successfully opened: {file_path}")
            return self.model
        else:
            print("Failed to open the document.")
            return None

    def disconnect(self):
        """Releases the COM object."""
        self.sw_app = None
        self.model = None
        print("Disconnected from SolidWorks.")