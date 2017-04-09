from collections import namedtuple


Freedom = namedtuple('Freedom', 'civilrights economy politicalfreedom')

Govt = namedtuple('Govt',
                  ('administration defence education environment healthcare'
                   ' commerce internationalaid lawandorder publictransport'
                   ' socialequality spirituality welfare'))

Dispatch = namedtuple('Dispatch', ('id title author category subcategory'
                                   ' created edited views score text'))

Sectors = namedtuple('Sectors', 'blackmarket government industry public')

CensusScale = namedtuple('CensusScale', 'info score rank prank rrank prrank')
CensusPoint = namedtuple('CensusPoint', 'info timestamp score')

Issue = namedtuple('Issue', ('id title author editor text options dismiss'))
IssueOption = namedtuple('IssueOption', ('text accept'))


class AuthenticationError(Exception):
    pass

