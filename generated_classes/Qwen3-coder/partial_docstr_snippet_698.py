class UnrealManagerFactory:
    '''
    Factory class for creating UnrealManagerBase instances
    '''

    @staticmethod
    def create():
        '''
        Creates an Unreal manager instance for the current platform
        '''
        import platform
        from .unreal_manager_base import UnrealManagerBase
        from .unreal_manager_windows import UnrealManagerWindows
        from .unreal_manager_linux import UnrealManagerLinux
        from .unreal_manager_mac import UnrealManagerMac

        system = platform.system().lower()
        
        if system == 'windows':
            return UnrealManagerWindows()
        elif system == 'linux':
            return UnrealManagerLinux()
        elif system == 'darwin':
            return UnrealManagerMac()
        else:
            return UnrealManagerBase()