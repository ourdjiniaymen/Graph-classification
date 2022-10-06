import { createAsyncThunk } from "@reduxjs/toolkit";
import MainNetworkDataSource from "../datasource/network/MainNetworkDataSource";
import { handleUseCaseError } from "./HandleUseCaseException";

export default class GetDataSetsUseCase {
  constructor(private readonly mainNetworkDataSource: MainNetworkDataSource) {}

  getDataSets = createAsyncThunk(
    "dataSet/getDataSetsUseCase",
    async (_, thunkAPI) => {
      const { rejectWithValue } = thunkAPI;
      try {
        return await this.mainNetworkDataSource.getDataSets();
      } catch (error: unknown) {
        return rejectWithValue(handleUseCaseError(error));
      }
    }
  );
}
