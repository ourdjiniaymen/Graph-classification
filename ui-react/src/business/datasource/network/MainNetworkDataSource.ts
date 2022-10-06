import Kernel from "../../domain/Kernel";
import DataSet from "../../domain/DataSet";
import Result from "../../domain/Result";
import RunClassification from "../../domain/RunClassification";

export default interface MainNetworkDataSource {
  getKernels(): Promise<Kernel[]>;
  getDataSets(): Promise<DataSet[]>;
  getResults(): Promise<Result[]>;
  runClassification(runClassification: RunClassification): Promise<Result>;
}
