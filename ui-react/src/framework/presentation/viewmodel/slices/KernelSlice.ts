import Kernel from "../../../../business/domain/Kernel";
import di from "../../../../di";
import { createSlice } from "@reduxjs/toolkit";
import { GetKernelsEvents } from "../events/GetKernelsEvents";

export interface KernelState {
  kernels: Kernel[];
  isLoadingKernel: boolean;
  error: string | null;
}

const initState: KernelState = {
  kernels: [],
  isLoadingKernel: false,
  error: null,
};

const kernelSlice = createSlice({
  name: "kernel",
  initialState: initState,
  reducers: {},
  extraReducers: (builder) => {
    //get kernels
    builder.addCase(
      di.GetKernelsUseCase.getKernels.pending,
      GetKernelsEvents().handlePending
    );
    builder.addCase(
      di.GetKernelsUseCase.getKernels.fulfilled,
      GetKernelsEvents().handleFulfilled
    );
    builder.addCase(
      di.GetKernelsUseCase.getKernels.rejected,
      GetKernelsEvents().handleRejected
    );
  },
});

export default kernelSlice.reducer;
