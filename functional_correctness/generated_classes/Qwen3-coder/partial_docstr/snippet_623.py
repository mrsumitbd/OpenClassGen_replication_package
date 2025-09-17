class InstrumentField:
    '''合约'''

    def __init__(self):
        '''Constructor'''
        self._instrument_id = ""
        self._exchange_id = ""
        self._instrument_name = ""
        self._product_id = ""
        self._product_class = ""
        self._delivery_year = 0
        self._delivery_month = 0
        self._max_market_order_volume = 0
        self._min_market_order_volume = 0
        self._max_limit_order_volume = 0
        self._min_limit_order_volume = 0
        self._volume_multiple = 0
        self._price_tick = 0.0
        self._create_date = ""
        self._open_date = ""
        self._expire_date = ""
        self._start_delivery_date = ""
        self._end_delivery_date = ""
        self._inst_life_phase = ""
        self._is_trading = False
        self._position_type = ""
        self._position_date_type = ""
        self._long_margin_ratio = 0.0
        self._short_margin_ratio = 0.0
        self._max_margin_side_algorithm = False

    def __str__(self):
        '''返回合约信息的字符串表示'''
        return f"InstrumentField(InstrumentID={self._instrument_id}, ExchangeID={self._exchange_id}, InstrumentName={self._instrument_name})"

    @property
    def __dict__(self):
        '''返回对象属性的字典表示'''
        return {
            'InstrumentID': self._instrument_id,
            'ExchangeID': self._exchange_id,
            'InstrumentName': self._instrument_name,
            'ProductID': self._product_id,
            'ProductClass': self._product_class,
            'DeliveryYear': self._delivery_year,
            'DeliveryMonth': self._delivery_month,
            'MaxMarketOrderVolume': self._max_market_order_volume,
            'MinMarketOrderVolume': self._min_market_order_volume,
            'MaxLimitOrderVolume': self._max_limit_order_volume,
            'MinLimitOrderVolume': self._min_limit_order_volume,
            'VolumeMultiple': self._volume_multiple,
            'PriceTick': self._price_tick,
            'CreateDate': self._create_date,
            'OpenDate': self._open_date,
            'ExpireDate': self._expire_date,
            'StartDeliveryDate': self._start_delivery_date,
            'EndDeliveryDate': self._end_delivery_date,
            'InstLifePhase': self._inst_life_phase,
            'IsTrading': self._is_trading,
            'PositionType': self._position_type,
            'PositionDateType': self._position_date_type,
            'LongMarginRatio': self._long_margin_ratio,
            'ShortMarginRatio': self._short_margin_ratio,
            'MaxMarginSideAlgorithm': self._max_margin_side_algorithm
        }

    @property
    def InstrumentID(self):
        return self._instrument_id

    @InstrumentID.setter
    def InstrumentID(self, value):
        self._instrument_id = value

    @property
    def ExchangeID(self):
        return self._exchange_id

    @ExchangeID.setter
    def ExchangeID(self, value):
        self._exchange_id = value

    @property
    def InstrumentName(self):
        return self._instrument_name

    @InstrumentName.setter
    def InstrumentName(self, value):
        self._instrument_name = value

    @property
    def ProductID(self):
        return self._product_id

    @ProductID.setter
    def ProductID(self, value):
        self._product_id = value

    @property
    def ProductClass(self):
        return self._product_class

    @ProductClass.setter
    def ProductClass(self, value):
        self._product_class = value

    @property
    def DeliveryYear(self):
        return self._delivery_year

    @DeliveryYear.setter
    def DeliveryYear(self, value):
        self._delivery_year = value

    @property
    def DeliveryMonth(self):
        return self._delivery_month

    @DeliveryMonth.setter
    def DeliveryMonth(self, value):
        self._delivery_month = value

    @property
    def MaxMarketOrderVolume(self):
        return self._max_market_order_volume

    @MaxMarketOrderVolume.setter
    def MaxMarketOrderVolume(self, value):
        self._max_market_order_volume = value

    @property
    def MinMarketOrderVolume(self):
        return self._min_market_order_volume

    @MinMarketOrderVolume.setter
    def MinMarketOrderVolume(self, value):
        self._min_market_order_volume = value

    @property
    def MaxLimitOrderVolume(self):
        return self._max_limit_order_volume

    @MaxLimitOrderVolume.setter
    def MaxLimitOrderVolume(self, value):
        self._max_limit_order_volume = value

    @property
    def MinLimitOrderVolume(self):
        return self._min_limit_order_volume

    @MinLimitOrderVolume.setter
    def MinLimitOrderVolume(self, value):
        self._min_limit_order_volume = value

    @property
    def VolumeMultiple(self):
        return self._volume_multiple

    @VolumeMultiple.setter
    def VolumeMultiple(self, value):
        self._volume_multiple = value

    @property
    def PriceTick(self):
        return self._price_tick

    @PriceTick.setter
    def PriceTick(self, value):
        self._price_tick = value

    @property
    def CreateDate(self):
        return self._create_date

    @CreateDate.setter
    def CreateDate(self, value):
        self._create_date = value

    @property
    def OpenDate(self):
        return self._open_date

    @OpenDate.setter
    def OpenDate(self, value):
        self._open_date = value

    @property
    def ExpireDate(self):
        return self._expire_date

    @ExpireDate.setter
    def ExpireDate(self, value):
        self._expire_date = value

    @property
    def StartDeliveryDate(self):
        return self._start_delivery_date

    @StartDeliveryDate.setter
    def StartDeliveryDate(self, value):
        self._start_delivery_date = value

    @property
    def EndDeliveryDate(self):
        return self._end_delivery_date

    @EndDeliveryDate.setter
    def EndDeliveryDate(self, value):
        self._end_delivery_date = value

    @property
    def InstLifePhase(self):
        return self._inst_life_phase

    @InstLifePhase.setter
    def InstLifePhase(self, value):
        self._inst_life_phase = value

    @property
    def IsTrading(self):
        return self._is_trading

    @IsTrading.setter
    def IsTrading(self, value):
        self._is_trading = value

    @property
    def PositionType(self):
        return self._position_type

    @PositionType.setter
    def PositionType(self, value):
        self._position_type = value

    @property
    def PositionDateType(self):
        return self._position_date_type

    @PositionDateType.setter
    def PositionDateType(self, value):
        self._position_date_type = value

    @property
    def LongMarginRatio(self):
        return self._long_margin_ratio

    @LongMarginRatio.setter
    def LongMarginRatio(self, value):
        self._long_margin_ratio = value

    @property
    def ShortMarginRatio(self):
        return self._short_margin_ratio

    @ShortMarginRatio.setter
    def ShortMarginRatio(self, value):
        self._short_margin_ratio = value

    @property
    def MaxMarginSideAlgorithm(self):
        return self._max_margin_side_algorithm

    @MaxMarginSideAlgorithm.setter
    def MaxMarginSideAlgorithm(self, value):
        self._max_margin_side_algorithm = value