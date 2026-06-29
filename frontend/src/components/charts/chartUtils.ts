import type { TimeseriesData } from "../../types";

export function buildChartRows(primary: TimeseriesData, secondary?: TimeseriesData) {
  return primary.steps.map((step, index) => ({
    step,
    pegPriceA: primary.peg_price[index],
    pegPriceB: secondary?.peg_price[index],
    collateralRatioA: primary.collateral_ratio[index],
    collateralRatioB: secondary?.collateral_ratio[index],
    reservesA: primary.reserves[index],
    reservesB: secondary?.reserves[index],
    supplyA: primary.supply[index],
    supplyB: secondary?.supply[index],
    mintVolume: primary.mint_volume[index],
    redeemVolume: primary.redeem_volume[index],
    liquidationVolume: primary.liquidation_volume[index],
  }));
}
