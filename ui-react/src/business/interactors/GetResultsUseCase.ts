import { createAsyncThunk } from "@reduxjs/toolkit";
import MainNetworkDataSource from "../datasource/network/MainNetworkDataSource";
import { handleUseCaseError } from "./HandleUseCaseException";

export default class GetResultsUseCase {
  constructor(private readonly mainNetworkDataSource: MainNetworkDataSource) {}

  getResults = createAsyncThunk(
    "result/getResultsUseCase",
    async (_, thunkAPI) => {
      const { rejectWithValue } = thunkAPI;
      try {
        return await this.mainNetworkDataSource.getResults();
      } catch (error: unknown) {
        return rejectWithValue(handleUseCaseError(error));
      }
    }
  );
}
