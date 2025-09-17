class InstrumentField:
    '''合约'''

    def __init__(self):
        '''Constructor'''
        self.InstrumentID = ""
        self.ExchangeID = ""
        self.InstrumentName = ""
        self.ExchangeInstID = ""
        self.ProductID = ""
        self.ProductClass = ""
        self.DeliveryYear = 0
        self.DeliveryMonth = 0
        self.MaxMarketOrderVolume = 0
        self.MinMarketOrderVolume = 0
        self.MaxLimitOrderVolume = 0
        self.MinLimitOrderVolume = 0
        self.VolumeMultiple = 0
        self.PriceTick = 0.0
        self.CreateDate = ""
        self.OpenDate = ""
        self.ExpireDate = ""
        self.StartDelivDate = ""
        self.EndDelivDate = ""
        self.InstLifePhase = ""
        self.IsTrading = 0
        self.PositionType = ""
        self.PositionDateType = ""
        self.LongMarginRatio = 0.0
        self.ShortMarginRatio = 0.0
        self.MaxMarginSideAlgorithm = ""
        self.UnderlyingInstrID = ""
        self.StrikePrice = 0.0
        self.OptionsType = ""
        self.UnderlyingMultiple = 0.0
        self.CombinationType = ""

    def __str__(self):
        ''''''
        return f"InstrumentField(InstrumentID={self.InstrumentID}, ExchangeID={self.ExchangeID}, InstrumentName={self.InstrumentName})"

    @property
    def __dict__(self):
        return {
            'InstrumentID': self.InstrumentID,
            'ExchangeID': self.ExchangeID,
            'InstrumentName': self.InstrumentName,
            'ExchangeInstID': self.ExchangeInstID,
            'ProductID': self.ProductID,
            'ProductClass': self.ProductClass,
            'DeliveryYear': self.DeliveryYear,
            'DeliveryMonth': self.DeliveryMonth,
            'MaxMarketOrderVolume': self.MaxMarketOrderVolume,
            'MinMarketOrderVolume': self.MinMarketOrderVolume,
            'MaxLimitOrderVolume': self.MaxLimitOrderVolume,
            'MinLimitOrderVolume': self.MinLimitOrderVolume,
            'VolumeMultiple': self.VolumeMultiple,
            'PriceTick': self.PriceTick,
            'CreateDate': self.CreateDate,
            'OpenDate': self.OpenDate,
            'ExpireDate': self.ExpireDate,
            'StartDelivDate': self.StartDelivDate,
            'EndDelivDate': self.EndDelivDate,
            'InstLifePhase': self.InstLifePhase,
            'IsTrading': self.IsTrading,
            'PositionType': self.PositionType,
            'PositionDateType': self.PositionDateType,
            'LongMarginRatio': self.LongMarginRatio,
            'ShortMarginRatio': self.ShortMarginRatio,
            'MaxMarginSideAlgorithm': self.MaxMarginSideAlgorithm,
            'UnderlyingInstrID': self.UnderlyingInstrID,
            'StrikePrice': self.StrikePrice,
            'OptionsType': self.OptionsType,
            'UnderlyingMultiple': self.UnderlyingMultiple,
            'CombinationType': self.CombinationType
        }