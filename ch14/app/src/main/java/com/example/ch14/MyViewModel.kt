package com.example.ch14

import android.graphics.Bitmap
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import java.io.InputStream

class MyViewModel: ViewModel() {
    private val itemsListData = MutableLiveData<ArrayList<Item>>()
    val items = ArrayList<Item>()

    fun addItem(item: Item) {
        items.add(item)
        itemsListData.value = items
    }
}