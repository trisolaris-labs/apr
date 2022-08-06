from gcc_utils import gccPrint
from utils import covalent
from utils.constants import (
    TRI_ADDRESS,
    TRIBAR_ADDRESS,
    WNEAR_ADDRESS,
    AURORA_ADDRESS,
    USDC_ADDRESS,
    USDT_ADDRESS,
    USN_ADDRESS,
    WETH_ADDRESS,
    WBTC_ADDRESS,
    ATLUNA_ADDRESS,
    ATUST_ADDRESS,
    FLX_ADDRESS,
    AVAX_ADDRESS,
    BNB_ADDRESS,
    MATIC_ADDRESS,
    META_ADDRESS,
    XNL_ADDRESS,
    GBA_ADDRESS,
    BBT_ADDRESS,
    BSTN_ADDRESS,
    ROSE_ADDRESS,
    SHITZU_ADDRESS,
    POLAR_ADDRESS,
    SPOLAR_ADDRESS,
    STNEAR_ADDRESS,
    LINEAR_ADDRESS,
    AUSDO_ADDRESS,
    ETHERNAL_ADDRESS,
    ORBITAL_ADDRESS,
    USP_ADDRESS,
    PLY_ADDRESS,
    SOLACE_ADDRESS,
    UMINT_ADDRESS,
    RUSD_ADDRESS,
    VWAVE_ADDRESS,
    BRRR_ADDRESS,
    ABR_ADDRESS,
    BIFI_ADDRESS,
    TRIPOLAR_ADDRESS,
    KSW_ADDRESS,
    PULP_ADDRESS,
    PEA_ADDRESS,
    DAI_ADDRESS,
    SMARTPAD_ADDRESS,
    NEARPAD_ADDRESS,
    CARBON_ADDRESS,
    ZOMB_ADDRESS,
    FAME_ADDRESS,
    HAK_ADDRESS,
    MFF_ADDRESS,
)
from utils.top_pools_utils import (
    create_base_pools_map,
    get_base_pairs_above_fee_threshold,
    to_checksum_address,
    token_pair_exists_in_base_pairs_map,
)

BASE_PAIRS = [
    [USDC_ADDRESS, WNEAR_ADDRESS],
    [USDT_ADDRESS, WNEAR_ADDRESS],
    [WNEAR_ADDRESS, WETH_ADDRESS],
    [WNEAR_ADDRESS, WBTC_ADDRESS],
    [SPOLAR_ADDRESS, WNEAR_ADDRESS],
    [AURORA_ADDRESS, WNEAR_ADDRESS],
    [WNEAR_ADDRESS, TRI_ADDRESS],
    [AUSDO_ADDRESS, USDT_ADDRESS],
    [WNEAR_ADDRESS, POLAR_ADDRESS],
    [BSTN_ADDRESS, WNEAR_ADDRESS],
    [USDT_ADDRESS, USDC_ADDRESS],
    [ETHERNAL_ADDRESS, WETH_ADDRESS],
    [USDT_ADDRESS, TRI_ADDRESS],
    [ORBITAL_ADDRESS, WBTC_ADDRESS],
    [AURORA_ADDRESS, WETH_ADDRESS],
    [WNEAR_ADDRESS, FLX_ADDRESS],
    [ATUST_ADDRESS, WNEAR_ADDRESS],
    [USP_ADDRESS, USDC_ADDRESS],
    [PLY_ADDRESS, WNEAR_ADDRESS],
    [STNEAR_ADDRESS, WNEAR_ADDRESS],
    [AURORA_ADDRESS, TRI_ADDRESS],
    [SOLACE_ADDRESS, WNEAR_ADDRESS],
    [UMINT_ADDRESS, WNEAR_ADDRESS],
    [RUSD_ADDRESS, WNEAR_ADDRESS],
    [VWAVE_ADDRESS, USDT_ADDRESS],
    [AVAX_ADDRESS, WNEAR_ADDRESS],
    [BRRR_ADDRESS, WNEAR_ADDRESS],
    [ABR_ADDRESS, USDC_ADDRESS],
    [BIFI_ADDRESS, WETH_ADDRESS],
    [STNEAR_ADDRESS, POLAR_ADDRESS],
    [VWAVE_ADDRESS, WNEAR_ADDRESS],
    [STNEAR_ADDRESS, TRI_ADDRESS],
    [TRIPOLAR_ADDRESS, TRI_ADDRESS],
    [VWAVE_ADDRESS, WETH_ADDRESS],
    [USDC_ADDRESS, WETH_ADDRESS],
    [WNEAR_ADDRESS, KSW_ADDRESS],
    [PULP_ADDRESS, PLY_ADDRESS],
    [META_ADDRESS, WNEAR_ADDRESS],
    [WNEAR_ADDRESS, ROSE_ADDRESS],
    [USDT_ADDRESS, GBA_ADDRESS],
    [PEA_ADDRESS, WNEAR_ADDRESS],
    [LINEAR_ADDRESS, WNEAR_ADDRESS],
    [ATUST_ADDRESS, WETH_ADDRESS],
    [WNEAR_ADDRESS, DAI_ADDRESS],
    [WETH_ADDRESS, TRI_ADDRESS],
    [WETH_ADDRESS, DAI_ADDRESS],
    [SHITZU_ADDRESS, USDC_ADDRESS],
    [USDT_ADDRESS, WETH_ADDRESS],
    [XNL_ADDRESS, AURORA_ADDRESS],
    [XNL_ADDRESS, WNEAR_ADDRESS],
    [BBT_ADDRESS, WNEAR_ADDRESS],
    [USDC_ADDRESS, DAI_ADDRESS],
    [SMARTPAD_ADDRESS, WNEAR_ADDRESS],
    [WETH_ADDRESS, WBTC_ADDRESS],
    [MATIC_ADDRESS, WNEAR_ADDRESS],
    [BSTN_ADDRESS, TRI_ADDRESS],
    [WETH_ADDRESS, FLX_ADDRESS],
    [USDT_ADDRESS, TRIBAR_ADDRESS],
    [BNB_ADDRESS, WNEAR_ADDRESS],
    [CARBON_ADDRESS, WNEAR_ADDRESS],
    [STNEAR_ADDRESS, TRIBAR_ADDRESS],
    [TRIPOLAR_ADDRESS, TRIBAR_ADDRESS],
    [USDC_ADDRESS, ZOMB_ADDRESS],
    [USDT_ADDRESS, FAME_ADDRESS],
    [USN_ADDRESS, USDC_ADDRESS],
    [ATUST_ADDRESS, ATLUNA_ADDRESS],
    [WNEAR_ADDRESS, ATLUNA_ADDRESS],
    [USDC_ADDRESS, TRI_ADDRESS],
    [NEARPAD_ADDRESS, WNEAR_ADDRESS],
    [USDC_ADDRESS, FAME_ADDRESS],
    [SHITZU_ADDRESS, WETH_ADDRESS],
    [HAK_ADDRESS, USDC_ADDRESS],
    [HAK_ADDRESS, WNEAR_ADDRESS],
    [PULP_ADDRESS, WNEAR_ADDRESS],
    [ATUST_ADDRESS, AURORA_ADDRESS],
    [ATUST_ADDRESS, MFF_ADDRESS],
    [SHITZU_ADDRESS, TRI_ADDRESS],
    [TRIBAR_ADDRESS, WNEAR_ADDRESS],
    [WNEAR_ADDRESS, ZOMB_ADDRESS],
    [MFF_ADDRESS, WETH_ADDRESS],
    [ATUST_ADDRESS, TRI_ADDRESS],
    [MATIC_ADDRESS, WETH_ADDRESS],
    [MFF_ADDRESS, USDC_ADDRESS],
]
TAG = "[TOP_POOLS_BASE]"

FEE_THRESHOLD = 1


def top_pools_base():
    gccPrint(f"{TAG} Starting")

    try:
        # Get pairs from Covalent API
        covalent_pools = covalent.getPools()
        base_pools_above_fee_threshold = get_base_pairs_above_fee_threshold(
            BASE_PAIRS, covalent_pools, FEE_THRESHOLD
        )
        gccPrint(
            f"{TAG} {len(base_pools_above_fee_threshold)} base pairs above fee threshold"
        )

        base_pairs_map = create_base_pools_map(base_pools_above_fee_threshold)

        covalent_pool_filters = (
            # Filter out pools below fee threshold
            lambda pool: pool["fee_24h_quote"] > FEE_THRESHOLD,
            # Filter out duplicate pools
            lambda pool: token_pair_exists_in_base_pairs_map(
                to_checksum_address(pool["token_0"]["contract_address"]),
                to_checksum_address(pool["token_1"]["contract_address"]),
                base_pairs_map,
            )
            is False,
        )

        covalent_pools = filter(
            lambda pool: all(f(pool) for f in covalent_pool_filters), covalent_pools
        )

        # Sort Covalent pools by fees DESC
        covalent_pools = sorted(
            covalent_pools, key=lambda x: x["fee_24h_quote"], reverse=True
        )

        # Get token pairs for valid Covalent pools
        covalent_pools = list(
            map(
                lambda pool: [
                    to_checksum_address(pool["token_0"]["contract_address"]),
                    to_checksum_address(pool["token_1"]["contract_address"]),
                ],
                covalent_pools,
            )
        )

        gccPrint(f"{TAG} {len(covalent_pools)} Covalent API pairs above fee threshold")

        # Combine valid base pools with top 20 fee-generating covalent pools
        top_pools_tokens = base_pools_above_fee_threshold + covalent_pools[0:20]

        gccPrint(f"{TAG} Completed with {len(top_pools_tokens)} pools")
        return top_pools_tokens
    except Exception as e:
        print("wat")
        gccPrint(
            f"{TAG} Error fetching from Covalent API; Returning BASE_PAIRS", "ERROR"
        )

        return BASE_PAIRS


if __name__ == "__main__":
    top_pools_base()
