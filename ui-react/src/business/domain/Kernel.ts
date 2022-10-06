import SelectOption from "./SelectOption";

export default interface Kernel {
  id: number;
  name: string;
  use_node_labels: boolean;
  use_node_attributes: boolean;
  parameters: string;
  parametersDetail: {
    name: string;
    values: number|null|string[];
  }[];
}

export const toSelectOptionKernel = (kernel: Kernel): SelectOption => {
  return {
    value: kernel.name,
    label: kernel.name,
  };
};
