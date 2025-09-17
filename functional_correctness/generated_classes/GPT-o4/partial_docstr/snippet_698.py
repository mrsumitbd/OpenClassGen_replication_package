class UnrealManagerFactory:
    '''
    Factory class for creating UnrealManagerBase instances
    '''

    @staticmethod
    def create():
        '''
        Creates an Unreal manager instance for the current platform
        '''
        platform = sys.platform
        if platform.startswith("win"):
            from unreal_manager.windows import WindowsUnrealManager
            return WindowsUnrealManager()
        elif platform.startswith("linux"):
            from unreal_manager.linux import LinuxUnrealManager
            return LinuxUnrealManager()
        elif platform == "darwin":
            from unreal_manager.mac import MacUnrealManager
            return MacUnrealManager()
        else:
            raise NotImplementedError(f"Unsupported platform: {platform}")