from dataclasses import dataclass


@dataclass
class SiteWideEvalContext:
    """
    Site-wide configuration passed into eval() calls on all layouts.
    """
    base_url: str
    title: str
    description: str
    protocol: str
