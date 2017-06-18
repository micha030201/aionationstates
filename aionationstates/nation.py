from aionationstates.utils import normalize, timestamp, banner_url
from aionationstates.types import (
    Freedom, FreedomScores, Govt, Sectors, NationZombie, DispatchThumbnail)
from aionationstates.session import Session, NS_URL, api_query
from aionationstates.shards import Census


class Nation(Census, Session):
    def __init__(self, id, *args, **kwargs):
        self.id = normalize(id)
        super().__init__(*args, **kwargs)

    def _call_api(self, params, **kwargs):
        params['nation'] = self.id
        return super()._call_api(params, **kwargs)


    @api_query('name')
    def name(root):
        return root.find('NAME').text

    @api_query('type')
    def type(root):
        return root.find('TYPE').text

    @api_query('fullname')
    def fullname(root):
        return root.find('FULLNAME').text

    @api_query('motto')
    def motto(root):
        return root.find('MOTTO').text  # TODO encoding mess

    @api_query('category')
    def category(root):
        return root.find('CATEGORY').text

    @api_query('region')
    def region(root):
        return root.find('REGION').text

    @api_query('animal')
    def animal(root):
        return root.find('ANIMAL').text

    @api_query('currency')
    def currency(root):
        return root.find('CURRENCY').text

    @api_query('demonym')
    def demonym(root):
        return root.find('DEMONYM').text

    @api_query('demonym2')
    def demonym2(root):
        return root.find('DEMONYM2').text

    @api_query('demonym2plural')
    def demonym2plural(root):
        return root.find('DEMONYM2PLURAL').text

    @api_query('flag')
    def flag(root):
        return root.find('FLAG').text

    @api_query('majorindustry')
    def majorindustry(root):
        return root.find('MAJORINDUSTRY').text

    @api_query('govtpriority')
    def govtpriority(root):
        return root.find('GOVTPRIORITY').text

    @api_query('lastactivity')
    def lastactivity(root):
        return root.find('LASTACTIVITY').text  # TODO there's no timestamp; decide

    @api_query('influence')
    def influence(root):
        return root.find('INFLUENCE').text

    @api_query('leader')
    def leader(root):
        return root.find('LEADER').text

    @api_query('capital')
    def capital(root):
        return root.find('CAPITAL').text

    @api_query('religion')
    def religion(root):
        return root.find('RELIGION').text

    @api_query('admirable')
    def admirable(root):
        return root.find('ADMIRABLE').text

    @api_query('animaltrait')
    def animaltrait(root):
        return root.find('ANIMALTRAIT').text

    @api_query('crime')
    def crime(root):
        return root.find('CRIME').text

    @api_query('govtdesc')
    def govtdesc(root):
        return root.find('GOVTDESC').text

    @api_query('industrydesc')
    def industrydesc(root):
        return root.find('INDUSTRYDESC').text

    @api_query('notable')
    def notable(root):
        return root.find('NOTABLE').text

    @api_query('sensibilities')
    def sensibilities(root):
        return root.find('SENSIBILITIES').text


    @api_query('population')
    def population(root):
        return int(root.find('POPULATION').text)

    @api_query('factbooks')
    def factbooks(root):
        return int(root.find('FACTBOOKS').text)

    @api_query('dispatches')
    def dispatches(root):
        return int(root.find('DISPATCHES').text)

    @api_query('gdp')
    def gdp(root):
        return int(root.find('GDP').text)

    @api_query('income')
    def income(root):
        return int(root.find('INCOME').text)

    @api_query('poorest')
    def poorest(root):
        return int(root.find('POOREST').text)

    @api_query('richest')
    def richest(root):
        return int(root.find('RICHEST').text)

    @api_query('foundedtime')
    def founded(root):
        return timestamp(root.find('FOUNDEDTIME').text)

    @api_query('firstlogin')
    def firstlogin(root):
        return timestamp(root.find('FIRSTLOGIN').text)

    @api_query('lastlogin')
    def lastlogin(root):
        return timestamp(root.find('LASTLOGIN').text)

    @api_query('wa')
    def wa(root):
        return root.find('UNSTATUS').text == 'WA Member'

    @api_query('banners')
    def banners(root):
        return [
            banner_url(elem.text)
            for elem in root.find('BANNERS')
        ]

    @api_query('freedom')
    def freedom(root):
        return Freedom(root.find('FREEDOM'))

    @api_query('freedomscores')
    def freedomscores(root):
        return FreedomScores(root.find('FREEDOMSCORES'))

    @api_query('govt')
    def govt(root):
        return Govt(root.find('GOVT'))

    @api_query('deaths')
    def deaths(root):
        return {
            elem.get('type'): float(elem.text)
            for elem in root.find('DEATHS')
        }

    @api_query('endorsements')
    def endorsements(root):
        text = root.find('ENDORSEMENTS').text
        return text.split(',') if text else ()

    @api_query('legislation')
    def legislation(root):
        return [elem.text for elem in root.find('LEGISLATION')]

    @api_query('sectors')
    def sectors(root):
        return Sectors(root.find('SECTORS'))

    @api_query('dispatchlist')
    def dispatchlist(root):
        return [
            DispatchThumbnail(elem)
            for elem in root.find('DISPATCHLIST')
        ]

    @api_query('zombie')
    def zombie(root):
        return NationZombie(root.find('ZOMBIE'))

    def verify(self, checksum, *, token=None):
        params = {'a': 'verify', 'checksum': checksum}
        if token:
            params['token'] = token
        # Needed so that we get output in xml, as opposed to
        # plain text. It doesn't actually matter what the
        # q param is, it's just important that it's not empty.
        @api_query('i_need_the_output_in_xml', **params)
        def result(root):
            return bool(int(root.find('VERIFY').text))
        return result(self)

    def verification_url(self, *, token=None):
        if token:
            return f'{NS_URL}page=verify_login?token={token}'
        return f'{NS_URL}page=verify_login'


