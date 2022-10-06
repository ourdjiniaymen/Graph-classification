export default interface RunClassification {
  kernel: string;
  dataset: string;
  rbf: boolean;
  sigma: number[];
  normalize: boolean;
  c: number[];
  cv: number;
  experiments: number;
  with_labels: boolean;
  with_attributes: boolean;
  parameters: {
    name: string;
    values: number[];
  }[];
}
