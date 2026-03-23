from ..schemas.optimization import OptimizationPageData


class OptimizationService:
    def build_optimize_page(self) -> OptimizationPageData:
        return OptimizationPageData()
