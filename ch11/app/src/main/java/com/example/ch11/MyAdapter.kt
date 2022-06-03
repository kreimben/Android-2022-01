package com.example.ch11

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.recyclerview.widget.RecyclerView
import com.example.ch11.databinding.ItemLayoutBinding

class MyAdapter(private val viewModel: MyViewModel) : RecyclerView.Adapter<MyAdapter.ViewHolder>() {

    inner class ViewHolder(val binding: ItemLayoutBinding) : RecyclerView.ViewHolder(binding.root) {
        fun setContents(pos: Int) {
            val item = viewModel.getItem(pos)
            binding.textView.text = item.name
            binding.textView2.text = item.name2
        }
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val layoutInflater = LayoutInflater.from(parent.context)
        val binding = ItemLayoutBinding.inflate(layoutInflater, parent, false)
        val vh = ViewHolder(binding)
        binding.root.setOnLongClickListener {
            viewModel.longClickItem = vh.adapterPosition
            false
        }
        return vh
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        holder.setContents(position)

    }

    override fun getItemCount() = viewModel.getSize()

}