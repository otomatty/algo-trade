"""
Algorithm parser module for backtest engine.

Related Documentation:
  └─ Plan: docs/03_plans/backtest/README.md

DEPENDENCY MAP:

Parents (Files that import this file):
  └─ src-python/modules/backtest/backtest_engine.py

Dependencies (External files that this file imports):
  ├─ typing (standard library)
  └─ src/types/algorithm (TypeScript types, used as reference)
"""
from typing import Dict, Any, List, Optional


class AlgorithmParser:
    """Parse algorithm definitions and evaluate trigger conditions."""
    
    def __init__(self):
        """Initialize algorithm parser."""
        pass
    
    def parse_algorithm(self, algorithm_definition: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse algorithm definition into executable format.
        
        Args:
            algorithm_definition: Algorithm definition dict with 'triggers' and 'actions'
        
        Returns:
            Parsed algorithm definition
        """
        if 'triggers' not in algorithm_definition or 'actions' not in algorithm_definition:
            raise ValueError("Algorithm definition must contain 'triggers' and 'actions'")
        
        return {
            'triggers': algorithm_definition['triggers'],
            'actions': algorithm_definition['actions']
        }
    
    def evaluate_trigger(
        self,
        trigger: Dict[str, Any],
        indicator_values: Dict[str, float],
        price_data: Dict[str, float]
    ) -> bool:
        """
        Evaluate a single trigger condition.
        
        Args:
            trigger: Trigger definition with 'type' and 'condition'
            indicator_values: Dict of indicator values (e.g., {'rsi': 65.5, 'macd': 0.5})
            price_data: Dict of price data (e.g., {'open': 100, 'high': 105, 'low': 95, 'close': 102, 'volume': 1000000})
        
        Returns:
            True if trigger condition is met, False otherwise
        """
        trigger_type = trigger.get('type', '').lower()
        condition = trigger.get('condition', {})
        
        if not condition:
            return False
        
        operator = condition.get('operator', '')
        value = condition.get('value')
        period = condition.get('period', 14)
        
        # Get the value to compare
        compare_value = None
        
        if trigger_type == 'rsi':
            compare_value = indicator_values.get('rsi')
        elif trigger_type == 'macd':
            compare_value = indicator_values.get('macd')
        elif trigger_type == 'price':
            compare_value = price_data.get('close')
        elif trigger_type == 'volume':
            compare_value = price_data.get('volume')
        elif trigger_type == 'moving_average':
            compare_value = indicator_values.get(f'ma_{period}')
        
        if compare_value is None:
            return False
        
        # Evaluate condition
        return self._evaluate_operator(operator, compare_value, value)
    
    def _evaluate_operator(self, operator: str, compare_value: float, target_value: Any) -> bool:
        """
        Evaluate comparison operator.
        
        Args:
            operator: Operator ('gt', 'lt', 'gte', 'lte', 'eq', 'between')
            compare_value: Value to compare
            target_value: Target value or range
        
        Returns:
            True if condition is met
        """
        if operator == 'gt':
            return compare_value > target_value
        elif operator == 'lt':
            return compare_value < target_value
        elif operator == 'gte':
            return compare_value >= target_value
        elif operator == 'lte':
            return compare_value <= target_value
        elif operator == 'eq':
            return abs(compare_value - target_value) < 0.0001  # Float comparison
        elif operator == 'between':
            if isinstance(target_value, list) and len(target_value) == 2:
                return target_value[0] <= compare_value <= target_value[1]
            return False
        else:
            return False
    
    def evaluate_triggers(
        self,
        triggers: List[Dict[str, Any]],
        indicator_values: Dict[str, float],
        price_data: Dict[str, float]
    ) -> bool:
        """
        Evaluate all triggers with logical operators.
        
        Args:
            triggers: List of trigger definitions
            indicator_values: Dict of indicator values
            price_data: Dict of price data
        
        Returns:
            True if all triggers are satisfied (AND logic by default)
        """
        if not triggers:
            return False
        
        results = []
        logical_operators = []
        
        for i, trigger in enumerate(triggers):
            result = self.evaluate_trigger(trigger, indicator_values, price_data)
            results.append(result)
            
            # Get logical operator (default to AND)
            if i < len(triggers) - 1:
                operator = trigger.get('logical_operator', 'AND')
                logical_operators.append(operator)
        
        # Evaluate with logical operators
        if len(results) == 1:
            return results[0]
        
        final_result = results[0]
        for i, operator in enumerate(logical_operators):
            if operator == 'AND':
                final_result = final_result and results[i + 1]
            elif operator == 'OR':
                final_result = final_result or results[i + 1]
            else:
                # Default to AND
                final_result = final_result and results[i + 1]
        
        return final_result

