export default interface Result {
  id: number;
  kernel: string;
  dataset: string;
  accuracy: number;
  standard_deviation: number;
  running_time: number;
  rbf: boolean;
  sigma: number | null;
  normalize: boolean;
  c: number;
  cv: number;
  experiments: number;
  with_labels: boolean;
  with_attributes: boolean;
  parameters: string;
}
