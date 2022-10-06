import Kernel from "../../../business/domain/Kernel";
import DataSet from "../../../business/domain/DataSet";
import Result from "../../../business/domain/Result";
import MainNetworkService from "./MainNetworkService";
import KernelDto, { toKernel } from "./model/KernelDto";
import DataSetDto, { toDataSet } from "./model/DataSetDto";
import ResultDto, { toResult } from "./model/ResultDto";
import RunClassification from "../../../business/domain/RunClassification";


export default class MainNetworkServiceImpl implements MainNetworkService {
  sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));

  async getKernels(): Promise<Kernel[]> {
    const res = await fetch("http://localhost:8000/kernels");
    console.log(res.json)
    return await res
      .json()
      .then((KernelDtos) => KernelDtos.map((val: KernelDto) => toKernel(val)));
  }

  async getDataSets(): Promise<DataSet[]> {
    const res = await fetch("http://localhost:8000/datasets");
    console.log(res.json)
    return await res
      .json()
      .then((DatasetDtos) => DatasetDtos.map((val: DataSetDto) => toDataSet(val)));
  }

  async getResults(): Promise<Result[]> {
    const res = await fetch("http://localhost:8000/logs");
    console.log(res.json)
    return await res
      .json()
      .then((ResultDtos) => ResultDtos.map((val: ResultDto) => toResult(val)));
  }

  async runClassification(
    runClassification: RunClassification
  ): Promise<Result> {
    console.log(JSON.stringify(runClassification))
    const res = await fetch("http://localhost:8000/add_evaluation/", {
      method: "POST",
      body: JSON.stringify(runClassification),
      headers: {
        "Content-type": "application/json; charset=UTF-8",
      },
    });
    return await res.json().then(result=>toResult(result));
  }
}
