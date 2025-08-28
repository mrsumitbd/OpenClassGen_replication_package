class UnrealManagerFactory:
    '''
    Factory class for creating UnrealManagerBase instances
    '''

    @staticmethod
    def create():
        '''
        Creates an Unreal manager instance for the current platform
        '''
        system = platform.system().lower()
        
        if system == 'windows':
            from .windows_unreal_manager import WindowsUnrealManager
            return WindowsUnrealManager()
        elif system == 'darwin':
            from .mac_unreal_manager import MacUnrealManager
            return MacUnrealManager()
        elif system == 'linux':
            from .linux_unreal_manager import LinuxUnrealManager
            return LinuxUnrealManager()
        else:
            raise NotImplementedError(f"Unreal manager not implemented for platform: {system}")