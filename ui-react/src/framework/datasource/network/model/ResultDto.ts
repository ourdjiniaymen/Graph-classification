import Result from "../../../../business/domain/Result";

export default interface ResultDto {
  id: number;
  kernel: string;
  dataset: string;
  accuracy: number;
  standard_deviation: number;
  running_time: number;
  rbf: boolean;
  sigma: number;
  normalize: boolean;
  c: number;
  cv: number;
  experiments: number;
  with_labels: boolean;
  with_attributes: boolean;
  parameters: {
    name: string;
    value: number;
  }[];
}

export const toResult = (resultDto: ResultDto): Result => {
  return {
    id: resultDto.id,
    kernel: resultDto.kernel,
    dataset: resultDto.dataset,
    accuracy: resultDto.accuracy,
    standard_deviation: resultDto.standard_deviation,
    running_time: resultDto.running_time,
    rbf: resultDto.rbf,
    sigma: resultDto.rbf ? resultDto.sigma : null,
    normalize: resultDto.normalize,
    c: resultDto.c,
    cv: resultDto.cv,
    experiments: resultDto.experiments,
    with_labels: resultDto.with_labels,
    with_attributes: resultDto.with_attributes,
    parameters: resultDto.parameters
      .map((parameter) => parameter.name + " : " + parameter.value)
      .join(" , "),
  };
};
