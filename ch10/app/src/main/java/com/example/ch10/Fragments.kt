package com.example.ch10

import android.app.AlertDialog
import android.app.Dialog
import android.os.Bundle
import android.view.View
import androidx.fragment.app.DialogFragment
import androidx.fragment.app.Fragment
import com.example.ch10.databinding.FragmentLayoutBinding

class MyDialogFragments : DialogFragment() {
    override fun onCreateDialog(savedInstanceState: Bundle?): Dialog {
        return AlertDialog.Builder(requireContext())
            .apply {
                setTitle("1991283")
                setMessage("김제환")
                setPositiveButton("OK") { dialog, id -> println("OK") }
            }
            .create()
    }
}

class HomeFragment : Fragment(R.layout.fragment_layout) {
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        val binding = FragmentLayoutBinding.bind(view)
        binding.textView.text = "HomeFragment"
    }
}

class Page1Fragment : Fragment(R.layout.fragment_layout) {
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        val binding = FragmentLayoutBinding.bind(view)
        binding.textView.text = "Page1Fragment"
    }
}

class Page2Fragment : Fragment(R.layout.fragment_layout) {
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        val binding = FragmentLayoutBinding.bind(view)
        binding.textView.text = "Page2Fragment"
    }
}