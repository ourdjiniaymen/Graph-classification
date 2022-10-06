import SelectOption from "./SelectOption";

export default interface DataSet {
  id: number;
  name: string;
  number_graphs: number;
  number_classes: number;
  classes_imbalance: number;
  average_nodes: number;
  average_edges: number;
  labels_number: number;
  attribute_dimension: number;
}

export const toSelectOptionDataSet = (dataSet: DataSet): SelectOption => {
  return {
    value: dataSet.name,
    label: dataSet.name,
  };
};
