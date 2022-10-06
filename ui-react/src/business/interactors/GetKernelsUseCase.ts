import { createAsyncThunk } from "@reduxjs/toolkit";
import MainNetworkDataSource from "../datasource/network/MainNetworkDataSource";
import { handleUseCaseError } from "./HandleUseCaseException";

export default class GetKernelsUseCase {
  constructor(private readonly mainNetworkDataSource: MainNetworkDataSource) {}

  getKernels = createAsyncThunk(
    "kernel/getKernelsUseCase",
    async (_, thunkAPI) => {
      const { rejectWithValue } = thunkAPI;
      try {
        return await this.mainNetworkDataSource.getKernels();
      } catch (error: unknown) {
        return rejectWithValue(handleUseCaseError(error));
      }
    }
  );
}
