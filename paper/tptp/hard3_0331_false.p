% hard3_0331  eq1=3092 eq2=3081  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(f(f(X,Y),Z),Y),W) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(f(f(X,Y),Y),Z),X) )).
