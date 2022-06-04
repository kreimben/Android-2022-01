package com.example.ch14

import android.Manifest
import android.content.ContentUris
import android.content.pm.PackageManager
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.os.Build
import android.provider.MediaStore
import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.core.content.ContextCompat.checkSelfPermission
import androidx.recyclerview.widget.RecyclerView
import com.example.ch14.databinding.RecyclerViewItemBinding

class MyAdapter(private val viewModel: MyViewModel) : RecyclerView.Adapter<MyAdapter.ViewHolder>() {

    inner class ViewHolder(private val binding: RecyclerViewItemBinding) :
        RecyclerView.ViewHolder(binding.root) {
        fun setContents(pos: Int) {
            with(viewModel.items[pos]) {
                binding.imageView.setImageBitmap(this.bitmap)
                binding.textView.text = this.text
            }
        }
    }

    override fun onCreateViewHolder(viewGroup: ViewGroup, viewType: Int): ViewHolder {
        val layoutInflater = LayoutInflater.from(viewGroup.context)
        val binding = RecyclerViewItemBinding.inflate(layoutInflater, viewGroup, false)
        return ViewHolder(binding)
    }

    override fun onBindViewHolder(viewHolder: ViewHolder, position: Int) {
        viewHolder.setContents(position)
    }

    fun addItem(item: Item) {
        viewModel.addItem(item)
    }

    override fun getItemCount() = viewModel.items.size
}

data class Item(val bitmap: Bitmap?, val text: String)