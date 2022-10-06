import MainNetworkService from "../../../framework/datasource/network/MainNetworkService";
import Kernel from "../../domain/Kernel";
import DataSet from "../../domain/DataSet";
import Result from "../../domain/Result";
import MainNetworkDataSource from "./MainNetworkDataSource";
import RunClassification from "../../domain/RunClassification";

export default class MainNetworkDataSourceImpl
  implements MainNetworkDataSource
{
  constructor(private readonly mainNetworkService: MainNetworkService) {}

  async getKernels(): Promise<Kernel[]> {
    return this.mainNetworkService.getKernels();
  }

  async getDataSets(): Promise<DataSet[]> {
    return this.mainNetworkService.getDataSets();
  }

  async getResults(): Promise<Result[]> {
    return this.mainNetworkService.getResults();
  }

  async runClassification(
    runClassification: RunClassification
  ): Promise<Result> {
    return this.mainNetworkService
      .runClassification(runClassification)
      .then((classification) => classification);
  }
}
