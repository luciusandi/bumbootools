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
    "fairprice-vinda": ProductConfig(
        slug="fairprice-vinda",
        brand="Vinda",
        description="PaVindaseo assortment at FairPrice",
        site_name="FairPrice",
        url="https://www.fairprice.com.sg/category/bathroom-tissues?filter=brand%3Avinda",
        extra_options={
            "api_url": (
                "https://website-api.omni.fairprice.com.sg/api/layout/category/v2?"
                "algopers=prm-ppb-1%2Cprm-ep-1%2Ct-epds-1%2Ct-ppb-0%2Ct-ep-0&"
                "category=bathroom-tissues&"
                "experiments=ls_deltime-sortA%2CsearchVariant-B%2Cgv-A%2Cshelflife-B%2Cds-A%2Cls_comsl-B%2C"
                "cartfiller-a%2Ccatnav-hide%2Ccatbubog-B%2Csbanner-A%2Ccount-b%2Ccam-a%2Cpromobanner-c%2C"
                "algopers-b%2Cdlv_pref_mf-B%2Cdelivery_pref_ffs-C%2Cdelivery_pref_pfc-C%2Ccrtalc-B%2C"
                "crt-v-wbble-A%2Czero_search_swimlane-A%2Csd-var-a%2CslotIncentive-eco%2Cosmos-on%2Cgsc-a%2C"
                "camp-lbl-B%2Cpoa-entry-A&filter=brand%3Avinda&includeTagDetails=true&"
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

import csv
import re
from pathlib import Path
from typing import List


def _default_dataset_path() -> Path:
    # dataset.csv is expected at the package root (one level up from this file)
    return Path(__file__).resolve().parents[1] / "dataset.csv"


def _slugify(value: str) -> str:
    value = (value or "").strip().lower()
    value = re.sub(r"[^\w]+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-")
    return value or "unknown"


def load_dataset_rows(path: str | None = None) -> List[dict]:
    """
    Parse `dataset.csv` and return raw rows as dictionaries.
    Columns expected (case-insensitive): Brand, Desc, Pack Size, Ply, Rolls, Sheets,
    Fairprice, Cold Storage, Redmart
    """
    dataset_path = Path(path) if path else _default_dataset_path()
    rows: List[dict] = []
    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset not found at {dataset_path}")
    with dataset_path.open(encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for r in reader:
            # normalize keys to simple names
            normalized = {k.strip(): (v or "").strip() for k, v in r.items()}
            rows.append(normalized)
    return rows


def load_dataset_products(path: str | None = None) -> List[ProductConfig]:
    """
    Convert parsed CSV rows into a list of `ProductConfig` instances, one per
    (site,brand) pair when a URL is provided.
    """
    rows = load_dataset_rows(path)
    products: List[ProductConfig] = []
    for row in rows:
        brand = row.get("Brand") or row.get("brand") or ""
        description = row.get("Desc") or row.get("description") or ""
        size = row.get("Pack Size") or None
        ply = row.get("Ply") or None
        extra_options = {}
        if row.get("Rolls"):
            extra_options["rolls"] = row.get("Rolls")
        if row.get("Sheets"):
            extra_options["sheets"] = row.get("Sheets")

        # iterate known site columns
        for col_name, site_name in (("Fairprice", "FairPrice"), ("Cold Storage", "Cold Storage"), ("Redmart", "RedMart")):
            url = row.get(col_name) or ""
            if not url or url.strip() in ("-", ""):
                continue
            site_slug = _slugify(site_name)
            brand_slug = _slugify(brand)
            slug = f"{site_slug}-{brand_slug}"
            prod = ProductConfig(
                slug=slug,
                brand=brand,
                description=description or f"{brand} assortment",
                site_name=site_name,
                url=url,
                size=size or None,
                ply=ply or None,
                extra_options=extra_options.copy(),
            )
            products.append(prod)
    return products


if __name__ == "__main__":  # pragma: no cover - simple CLI
    # Quick CLI to preview parsed rows for manual testing
    import sys

    try:
        preview = load_dataset_products()
    except Exception as exc:
        print(f"Could not load dataset: {exc}", file=sys.stderr)
        raise SystemExit(1)
    for p in preview[:20]:
        print(f"{p.slug}\t{p.site_name}\t{p.brand}\t{p.size}\t{p.ply}\t{p.url}")

