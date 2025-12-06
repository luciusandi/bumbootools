"""Static catalog describing each brand/variant/site combination."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable


@dataclass(frozen=True, slots=True)
class ProductConfig:
    """
    Defines a single scrape target (brand + size + ply at a specific site).
    """

    slug: str
    brand: str
    description: str
    site_name: str
    url: str
    size: str | None = None
    ply: str | None = None
    extra_options: dict[str, str] = field(default_factory=dict)


PRODUCT_CATALOG: dict[str, ProductConfig] = {
    "example-ultra-soft": ProductConfig(
        slug="example-ultra-soft",
        brand="Example Brand",
        description="Ultra Soft Mega Pack",
        site_name="Example Store",
        url="https://example.com/toilet-paper",
        size="24 Mega Rolls",
        ply="3",
        extra_options={
            "total_reviews": "1500",
            "total_rating": "4.9",
            "price": "24.99",
        },
    ),
    "coldstorage-kleenex": ProductConfig(
        slug="coldstorage-kleenex",
        brand="Kleenex",
        description="Kleenex assortment at Cold Storage",
        site_name="Cold Storage",
        url="https://coldstorage.com.sg/en/category/100013-100174-101066/1.html?proCatId=1&proId=32643",
    ),
    "coldstorage-nootrees": ProductConfig(
        slug="coldstorage-nootrees",
        brand="Nootrees",
        description="Nootrees assortment at Cold Storage",
        site_name="Cold Storage",
        url="https://coldstorage.com.sg/en/category/100013-100174-101066/1.html?proCatId=1&proId=46847",
    ),
    "coldstorage-paseo": ProductConfig(
        slug="coldstorage-paseo",
        brand="Paseo",
        description="Paseo assortment at Cold Storage",
        site_name="Cold Storage",
        url="https://coldstorage.com.sg/en/category/100013-100174-101066/1.html?proCatId=1&proId=42272",
    ),
    "coldstorage-pursoft": ProductConfig(
        slug="coldstorage-pursoft",
        brand="Pursoft",
        description="Pursoft assortment at Cold Storage",
        site_name="Cold Storage",
        url="https://coldstorage.com.sg/en/category/100013-100174-101066/1.html?proCatId=1&proId=48698",
    ),
    "coldstorage-vinda": ProductConfig(
        slug="coldstorage-vinda",
        brand="Vinda",
        description="Vinda assortment at Cold Storage",
        site_name="Cold Storage",
        url="https://coldstorage.com.sg/en/category/100013-100174-101066/1.html?proCatId=1&proId=33232",
    ),
    "coldstorage-tempo": ProductConfig(
        slug="coldstorage-tempo",
        brand="Tempo",
        description="Tempo assortment at Cold Storage",
        site_name="Cold Storage",
        url="https://coldstorage.com.sg/en/category/100013-100174-101066/1.html?proCatId=1&proId=32949",
    ),
    "coldstorage-cloversoft": ProductConfig(
        slug="coldstorage-cloversoft",
        brand="Cloversoft",
        description="Cloversoft assortment at Cold Storage",
        site_name="Cold Storage",
        url="https://coldstorage.com.sg/en/category/100013-100174-101066/1.html?proCatId=1&proId=45287",
    ),
    "fairprice-kleenex": ProductConfig(
        slug="fairprice-kleenex",
        brand="Kleenex",
        description="Kleenex assortment at FairPrice",
        site_name="FairPrice",
        url="https://www.fairprice.com.sg/category/bathroom-tissues?filter=brand%3Akleenex",
        extra_options={
            "api_url": (
                "https://website-api.omni.fairprice.com.sg/api/layout/category/v2?"
                "algopers=prm-ppb-1%2Cprm-ep-1%2Ct-epds-1%2Ct-ppb-0%2Ct-ep-0&"
                "category=bathroom-tissues&"
                "experiments=ls_deltime-sortA%2CsearchVariant-B%2Cgv-A%2Cshelflife-B%2Cds-A%2Cls_comsl-B%2C"
                "cartfiller-a%2Ccatnav-hide%2Ccatbubog-B%2Csbanner-A%2Ccount-b%2Ccam-a%2Cpromobanner-c%2C"
                "algopers-b%2Cdlv_pref_mf-B%2Cdelivery_pref_ffs-C%2Cdelivery_pref_pfc-C%2Ccrtalc-B%2C"
                "crt-v-wbble-A%2Czero_search_swimlane-A%2Csd-var-a%2CslotIncentive-eco%2Cosmos-on%2Cgsc-a%2C"
                "camp-lbl-B%2Cpoa-entry-A&filter=brand%3Akleenex&includeTagDetails=true&"
                "orderType=DELIVERY&page={page}&url=bathroom-tissues"
            )
        },
    ),
    "fairprice-paseo": ProductConfig(
        slug="fairprice-paseo",
        brand="Paseo",
        description="Paseo assortment at FairPrice",
        site_name="FairPrice",
        url="https://www.fairprice.com.sg/category/bathroom-tissues?filter=brand%3Apaseo",
        extra_options={
            "api_url": (
                "https://website-api.omni.fairprice.com.sg/api/layout/category/v2?"
                "algopers=prm-ppb-1%2Cprm-ep-1%2Ct-epds-1%2Ct-ppb-0%2Ct-ep-0&"
                "category=bathroom-tissues&"
                "experiments=ls_deltime-sortA%2CsearchVariant-B%2Cgv-A%2Cshelflife-B%2Cds-A%2Cls_comsl-B%2C"
                "cartfiller-a%2Ccatnav-hide%2Ccatbubog-B%2Csbanner-A%2Ccount-b%2Ccam-a%2Cpromobanner-c%2C"
                "algopers-b%2Cdlv_pref_mf-B%2Cdelivery_pref_ffs-C%2Cdelivery_pref_pfc-C%2Ccrtalc-B%2C"
                "crt-v-wbble-A%2Czero_search_swimlane-A%2Csd-var-a%2CslotIncentive-eco%2Cosmos-on%2Cgsc-a%2C"
                "camp-lbl-B%2Cpoa-entry-A&filter=brand%3Apaseo&includeTagDetails=true&"
                "orderType=DELIVERY&page={page}&url=bathroom-tissues"
            )
        },
    ),
    "fairprice-pursoft": ProductConfig(
        slug="fairprice-pursoft",
        brand="Pursoft",
        description="Pursoft assortment at FairPrice",
        site_name="FairPrice",
        url="https://www.fairprice.com.sg/category/bathroom-tissues?filter=brand%3Apursoft",
        extra_options={
            "api_url": (
                "https://website-api.omni.fairprice.com.sg/api/layout/category/v2?"
                "algopers=prm-ppb-1%2Cprm-ep-1%2Ct-epds-1%2Ct-ppb-0%2Ct-ep-0&"
                "category=bathroom-tissues&"
                "experiments=ls_deltime-sortA%2CsearchVariant-B%2Cgv-A%2Cshelflife-B%2Cds-A%2Cls_comsl-B%2C"
                "cartfiller-a%2Ccatnav-hide%2Ccatbubog-B%2Csbanner-A%2Ccount-b%2Ccam-a%2Cpromobanner-c%2C"
                "algopers-b%2Cdlv_pref_mf-B%2Cdelivery_pref_ffs-C%2Cdelivery_pref_pfc-C%2Ccrtalc-B%2C"
                "crt-v-wbble-A%2Czero_search_swimlane-A%2Csd-var-a%2CslotIncentive-eco%2Cosmos-on%2Cgsc-a%2C"
                "camp-lbl-B%2Cpoa-entry-A&filter=brand%3Apursoft&includeTagDetails=true&"
                "orderType=DELIVERY&page={page}&url=bathroom-tissues"
            )
        },
    ),
    "fairprice-fairprice": ProductConfig(
        slug="fairprice-fairprice",
        brand="FairPrice",
        description="FairPrice house-brand bathroom tissues",
        site_name="FairPrice",
        url="https://www.fairprice.com.sg/category/bathroom-tissues?filter=brand%3Afairprice",
        extra_options={
            "api_url": (
                "https://website-api.omni.fairprice.com.sg/api/layout/category/v2?"
                "algopers=prm-ppb-1%2Cprm-ep-1%2Ct-epds-1%2Ct-ppb-0%2Ct-ep-0&"
                "category=bathroom-tissues&"
                "experiments=ls_deltime-sortA%2CsearchVariant-B%2Cgv-A%2Cshelflife-B%2Cds-A%2Cls_comsl-B%2C"
                "cartfiller-a%2Ccatnav-hide%2Ccatbubog-B%2Csbanner-A%2Ccount-b%2Ccam-a%2Cpromobanner-c%2C"
                "algopers-b%2Cdlv_pref_mf-B%2Cdelivery_pref_ffs-C%2Cdelivery_pref_pfc-C%2Ccrtalc-B%2C"
                "crt-v-wbble-A%2Czero_search_swimlane-A%2Csd-var-a%2CslotIncentive-eco%2Cosmos-on%2Cgsc-a%2C"
                "camp-lbl-B%2Cpoa-entry-A&filter=brand%3Afairprice&includeTagDetails=true&"
                "orderType=DELIVERY&page={page}&url=bathroom-tissues"
            )
        },
    ),
    "fairprice-beautex": ProductConfig(
        slug="fairprice-beautex",
        brand="Beautex",
        description="Beautex assortment at FairPrice",
        site_name="FairPrice",
        url="https://www.fairprice.com.sg/category/bathroom-tissues?filter=brand%3Abeautex",
        extra_options={
            "api_url": (
                "https://website-api.omni.fairprice.com.sg/api/layout/category/v2?"
                "algopers=prm-ppb-1%2Cprm-ep-1%2Ct-epds-1%2Ct-ppb-0%2Ct-ep-0&"
                "category=bathroom-tissues&"
                "experiments=ls_deltime-sortA%2CsearchVariant-B%2Cgv-A%2Cshelflife-B%2Cds-A%2Cls_comsl-B%2C"
                "cartfiller-a%2Ccatnav-hide%2Ccatbubog-B%2Csbanner-A%2Ccount-b%2Ccam-a%2Cpromobanner-c%2C"
                "algopers-b%2Cdlv_pref_mf-B%2Cdelivery_pref_ffs-C%2Cdelivery_pref_pfc-C%2Ccrtalc-B%2C"
                "crt-v-wbble-A%2Czero_search_swimlane-A%2Csd-var-a%2CslotIncentive-eco%2Cosmos-on%2Cgsc-a%2C"
                "camp-lbl-B%2Cpoa-entry-A&filter=brand%3Abeautex&includeTagDetails=true&"
                "orderType=DELIVERY&page={page}&url=bathroom-tissues"
            )
        },
    ),
    "fairprice-neutra": ProductConfig(
        slug="fairprice-neutra",
        brand="Neutra",
        description="Neutra assortment at FairPrice",
        site_name="FairPrice",
        url="https://www.fairprice.com.sg/category/bathroom-tissues?filter=brand%3Aneutra",
        extra_options={
            "api_url": (
                "https://website-api.omni.fairprice.com.sg/api/layout/category/v2?"
                "algopers=prm-ppb-1%2Cprm-ep-1%2Ct-epds-1%2Ct-ppb-0%2Ct-ep-0&"
                "category=bathroom-tissues&"
                "experiments=ls_deltime-sortA%2CsearchVariant-B%2Cgv-A%2Cshelflife-B%2Cds-A%2Cls_comsl-B%2C"
                "cartfiller-a%2Ccatnav-hide%2Ccatbubog-B%2Csbanner-A%2Ccount-b%2Ccam-a%2Cpromobanner-c%2C"
                "algopers-b%2Cdlv_pref_mf-B%2Cdelivery_pref_ffs-C%2Cdelivery_pref_pfc-C%2Ccrtalc-B%2C"
                "crt-v-wbble-A%2Czero_search_swimlane-A%2Csd-var-a%2CslotIncentive-eco%2Cosmos-on%2Cgsc-a%2C"
                "camp-lbl-B%2Cpoa-entry-A&filter=brand%3Aneutra&includeTagDetails=true&"
                "orderType=DELIVERY&page={page}&url=bathroom-tissues"
            )
        },
    ),
    "fairprice-cloversoft": ProductConfig(
        slug="fairprice-cloversoft",
        brand="Cloversoft",
        description="Cloversoft assortment at FairPrice",
        site_name="FairPrice",
        url="https://www.fairprice.com.sg/category/bathroom-tissues?filter=brand%3Acloversoft",
        extra_options={
            "api_url": (
                "https://website-api.omni.fairprice.com.sg/api/layout/category/v2?"
                "algopers=prm-ppb-1%2Cprm-ep-1%2Ct-epds-1%2Ct-ppb-0%2Ct-ep-0&"
                "category=bathroom-tissues&"
                "experiments=ls_deltime-sortA%2CsearchVariant-B%2Cgv-A%2Cshelflife-B%2Cds-A%2Cls_comsl-B%2C"
                "cartfiller-a%2Ccatnav-hide%2Ccatbubog-B%2Csbanner-A%2Ccount-b%2Ccam-a%2Cpromobanner-c%2C"
                "algopers-b%2Cdlv_pref_mf-B%2Cdelivery_pref_ffs-C%2Cdelivery_pref_pfc-C%2Ccrtalc-B%2C"
                "crt-v-wbble-A%2Czero_search_swimlane-A%2Csd-var-a%2CslotIncentive-eco%2Cosmos-on%2Cgsc-a%2C"
                "camp-lbl-B%2Cpoa-entry-A&filter=brand%3Acloversoft&includeTagDetails=true&"
                "orderType=DELIVERY&page={page}&url=bathroom-tissues"
            )
        },
    ),
    "fairprice-nootrees": ProductConfig(
        slug="fairprice-nootrees",
        brand="Nootrees",
        description="Nootrees assortment at FairPrice",
        site_name="FairPrice",
        url="https://www.fairprice.com.sg/category/bathroom-tissues?filter=brand%3Anootrees",
        extra_options={
            "api_url": (
                "https://website-api.omni.fairprice.com.sg/api/layout/category/v2?"
                "algopers=prm-ppb-1%2Cprm-ep-1%2Ct-epds-1%2Ct-ppb-0%2Ct-ep-0&"
                "category=bathroom-tissues&"
                "experiments=ls_deltime-sortA%2CsearchVariant-B%2Cgv-A%2Cshelflife-B%2Cds-A%2Cls_comsl-B%2C"
                "cartfiller-a%2Ccatnav-hide%2Ccatbubog-B%2Csbanner-A%2Ccount-b%2Ccam-a%2Cpromobanner-c%2C"
                "algopers-b%2Cdlv_pref_mf-B%2Cdelivery_pref_ffs-C%2Cdelivery_pref_pfc-C%2Ccrtalc-B%2C"
                "crt-v-wbble-A%2Czero_search_swimlane-A%2Csd-var-a%2CslotIncentive-eco%2Cosmos-on%2Cgsc-a%2C"
                "camp-lbl-B%2Cpoa-entry-A&filter=brand%3Anootrees&includeTagDetails=true&"
                "orderType=DELIVERY&page={page}&url=bathroom-tissues"
            )
        },
    ),
    "fairprice-tempo": ProductConfig(
        slug="fairprice-tempo",
        brand="Tempo",
        description="Tempo assortment at FairPrice",
        site_name="FairPrice",
        url="https://www.fairprice.com.sg/category/bathroom-tissues?filter=brand%3Atempo",
        extra_options={
            "api_url": (
                "https://website-api.omni.fairprice.com.sg/api/layout/category/v2?"
                "algopers=prm-ppb-1%2Cprm-ep-1%2Ct-epds-1%2Ct-ppb-0%2Ct-ep-0&"
                "category=bathroom-tissues&"
                "experiments=ls_deltime-sortA%2CsearchVariant-B%2Cgv-A%2Cshelflife-B%2Cds-A%2Cls_comsl-B%2C"
                "cartfiller-a%2Ccatnav-hide%2Ccatbubog-B%2Csbanner-A%2Ccount-b%2Ccam-a%2Cpromobanner-c%2C"
                "algopers-b%2Cdlv_pref_mf-B%2Cdelivery_pref_ffs-C%2Cdelivery_pref_pfc-C%2Ccrtalc-B%2C"
                "crt-v-wbble-A%2Czero_search_swimlane-A%2Csd-var-a%2CslotIncentive-eco%2Cosmos-on%2Cgsc-a%2C"
                "camp-lbl-B%2Cpoa-entry-A&filter=brand%3Atempo&includeTagDetails=true&"
                "orderType=DELIVERY&page={page}&url=bathroom-tissues"
            )
        },
    ),
    "redmart-tempo": ProductConfig(
        slug="redmart-tempo",
        brand="Tempo",
        description="Tempo assortment at RedMart",
        site_name="RedMart",
        url="https://redmart.lazada.sg/shop-groceries-laundry-household-paper/tem-po/?m=redmart",
        extra_options={
            "api_url": "https://redmart.lazada.sg/shop-groceries-laundry-household-paper/tem-po/?ajax=true&m=redmart"
        },
    ),
    "redmart-kleenex": ProductConfig(
        slug="redmart-kleenex",
        brand="Kleenex",
        description="Kleenex assortment at RedMart",
        site_name="RedMart",
        url="https://redmart.lazada.sg/shop-groceries-laundry-household-paper/kleenex/?m=redmart",
        extra_options={
            "api_url": "https://redmart.lazada.sg/shop-groceries-laundry-household-paper/kleenex/?ajax=true&m=redmart"
        },
    ),
    "redmart-pursoft": ProductConfig(
        slug="redmart-pursoft",
        brand="Pursoft",
        description="Pursoft assortment at RedMart",
        site_name="RedMart",
        url="https://redmart.lazada.sg/shop-groceries-laundry-household-paper/pursoft/?m=redmart",
        extra_options={
            "api_url": "https://redmart.lazada.sg/shop-groceries-laundry-household-paper/pursoft/?ajax=true&m=redmart"
        },
    ),
    "redmart-vinda": ProductConfig(
        slug="redmart-vinda",
        brand="Vinda",
        description="Vinda assortment at RedMart",
        site_name="RedMart",
        url="https://redmart.lazada.sg/shop-groceries-laundry-household-paper/vin-da/?m=redmart",
        extra_options={
            "api_url": "https://redmart.lazada.sg/shop-groceries-laundry-household-paper/vin-da/?ajax=true&m=redmart"
        },
    ),
    "redmart-beautex": ProductConfig(
        slug="redmart-beautex",
        brand="Beautex",
        description="Beautex assortment at RedMart",
        site_name="RedMart",
        url="https://redmart.lazada.sg/shop-groceries-laundry-household-paper/?m=redmart",
        extra_options={
            "api_url": "https://redmart.lazada.sg/shop-groceries-laundry-household-paper/beautex/?ajax=true&m=redmart"
        },
    ),
    "redmart-paseo": ProductConfig(
        slug="redmart-paseo",
        brand="Paseo",
        description="Paseo assortment at RedMart",
        site_name="RedMart",
        url="https://redmart.lazada.sg/shop-groceries-laundry-household-paper/?m=redmart",
        extra_options={
            "api_url": "https://redmart.lazada.sg/shop-groceries-laundry-household-paper/paseo_1/?ajax=true&m=redmart"
        },
    ),
    "redmart-cloversoft": ProductConfig(
        slug="redmart-cloversoft",
        brand="Cloversoft",
        description="Cloversoft assortment at RedMart",
        site_name="RedMart",
        url="https://redmart.lazada.sg/shop-groceries-laundry-household-paper/?m=redmart",
        extra_options={
            "api_url": "https://redmart.lazada.sg/shop-groceries-laundry-household-paper/cloversoft/?ajax=true&m=redmart"
        },
    ),
    "redmart-nootrees": ProductConfig(
        slug="redmart-nootrees",
        brand="Nootrees",
        description="Nootrees assortment at RedMart",
        site_name="RedMart",
        url="https://redmart.lazada.sg/shop-groceries-laundry-household-paper/nootrees/?m=redmart",
        extra_options={
            "api_url": "https://redmart.lazada.sg/shop-groceries-laundry-household-paper/nootrees/?ajax=true&m=redmart"
        },
    ),
}


def get_product(slug: str) -> ProductConfig:
    try:
        return PRODUCT_CATALOG[slug]
    except KeyError as exc:
        msg = f"Product '{slug}' is not defined in the catalog"
        raise KeyError(msg) from exc


def list_products() -> Iterable[ProductConfig]:
    return PRODUCT_CATALOG.values()

