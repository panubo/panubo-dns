from dnsmanager.recipes import NameServerRecipe, MxRecipe


class VoltGridEmail(MxRecipe):
    data = [
        ('10', 'mail.voltgrid.com.'),
    ]


class VoltGridNameServers(NameServerRecipe):
    data = ('ns1.voltgrid.com.', 'ns2.voltgrid.com.', 'ns3.voltgrid.com.')


class CromovaNameServers(NameServerRecipe):
    data = ('ns1.cromova.net.', 'ns2.cromova.net.')


class PanuboNameServers(NameServerRecipe):
    data = ('ns1.panubo.net.', 'ns2.panubo.net.', 'ns3.panubo.net.')
