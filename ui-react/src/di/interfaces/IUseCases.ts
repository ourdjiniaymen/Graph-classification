import GetKernelsUseCase from "../../business/interactors/GetKernelsUseCase";
import GetDataSetsUseCase from "../../business/interactors/GetDataSetsUseCase";
import GetResultsUseCase from "../../business/interactors/GetResultsUseCase";
import RunClassificationUseCase from "../../business/interactors/RunClassificationUseCase";

export default interface IUseCases {
  GetKernelsUseCase: GetKernelsUseCase;
  GetDataSetsUseCase: GetDataSetsUseCase;
  GetResultsUseCase: GetResultsUseCase;
  RunClassificationUseCase: RunClassificationUseCase;
}
