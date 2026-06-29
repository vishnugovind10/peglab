from peglab_engine.models.base import CollateralModel
from peglab_engine.models.crypto_backed import CryptoBackedModel
from peglab_engine.models.fiat_backed import FiatBackedModel
from peglab_engine.models.overcollateralized import OvercollateralizedModel

MODEL_REGISTRY: dict[str, type[CollateralModel]] = {
    FiatBackedModel.model_id: FiatBackedModel,
    CryptoBackedModel.model_id: CryptoBackedModel,
    OvercollateralizedModel.model_id: OvercollateralizedModel,
}

__all__ = [
    "CollateralModel",
    "CryptoBackedModel",
    "FiatBackedModel",
    "MODEL_REGISTRY",
    "OvercollateralizedModel",
]
