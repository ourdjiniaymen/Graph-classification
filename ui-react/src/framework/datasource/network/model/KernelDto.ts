import Kernel from "../../../../business/domain/Kernel";

export default interface KernelDto {
  id: number;
  name: string;
  use_node_labels: boolean;
  use_node_attributes: boolean;
  parameters: {
    name: string;
    values: number[];
  }[];
}

export const toKernel = (kernelDto: KernelDto): Kernel => {
  return {
    id: kernelDto.id,
    name: kernelDto.name,
    use_node_labels: kernelDto.use_node_labels,
    use_node_attributes: kernelDto.use_node_attributes,
    parameters: kernelDto.parameters
      .map((parameter) => parameter.name)
      .join(" , "),
    parametersDetail: kernelDto.parameters,
  };
};
