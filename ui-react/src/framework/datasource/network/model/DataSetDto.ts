import DataSet from "../../../../business/domain/DataSet";

export default interface DataSetDto {
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

export const toDataSet = (dataSetDto: DataSetDto): DataSet => {
  return {
    id: dataSetDto.id,
    name: dataSetDto.name,
    number_graphs: dataSetDto.number_graphs,
    number_classes: dataSetDto.number_classes,
    classes_imbalance: dataSetDto.classes_imbalance,
    average_nodes: dataSetDto.average_nodes,
    average_edges: dataSetDto.average_edges,
    labels_number: dataSetDto.labels_number,
    attribute_dimension: dataSetDto.attribute_dimension,
  };
};
