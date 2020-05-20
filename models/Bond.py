class Bond:
    def __init__(self, id, user, flavor, tickerSymbol, ticker, currency, issueDate, originalIssueDate, firstCouponDate, coupon, maturityDate, auctionDate, isin, totalIssueSize):
        self.id = id
        self.user = user
        self.flavor = flavor
        self.tickerSymbol = tickerSymbol
        self.ticker = ticker
        self.currency = currency
        self.issueDate = issueDate
        self.originalIssueDate = originalIssueDate
        self.firstCouponDate = firstCouponDate
        self.coupon = coupon
        self.maturityDate = maturityDate
        self.auctionDate = auctionDate
        self.isin = isin,
        self.totalIssueSize = totalIssueSize