import { createAsyncThunk, PayloadAction } from "@reduxjs/toolkit";
import Kernel from "../../../../business/domain/Kernel";
import di from "../../../../di";
import { KernelState } from "../slices/KernelSlice";

export const GetKernelsEvents = () => {
  const getKernelsEvent = createAsyncThunk(
    "kernel/getKernelsEvent",
    async (_, thunkAPI) => {
      const { dispatch } = thunkAPI;
      dispatch(di.GetKernelsUseCase.getKernels());
    }
  );

  const handlePending = (state: KernelState) => {
    state.isLoadingKernel = true;
    state.error = null;
  };

  const handleFulfilled = (
    state: KernelState,
    action: PayloadAction<Kernel[]>
  ) => {
    state.isLoadingKernel = false;
    state.kernels = action.payload;
  };

  const handleRejected = (
    state: KernelState,
    action: PayloadAction<unknown>
  ) => {
    state.isLoadingKernel = false;
    state.error = action.payload as string;
  };
  return {
    getKernelsEvent,
    handlePending,
    handleFulfilled,
    handleRejected,
  };
};
