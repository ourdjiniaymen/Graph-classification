import Kernel from "../../../business/domain/Kernel";
import DataSet from "../../../business/domain/DataSet";
import Result from "../../../business/domain/Result";
import RunClassification from "../../../business/domain/RunClassification";

export default interface MainNetworkService {
  getKernels(): Promise<Kernel[]>;
  getDataSets(): Promise<DataSet[]>;
  getResults(): Promise<Result[]>;
  runClassification(runClassification: RunClassification): Promise<Result>;
}
