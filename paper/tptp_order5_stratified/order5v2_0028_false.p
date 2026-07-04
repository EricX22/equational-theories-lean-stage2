% order5v2_0028  eq1=36879 eq2=27096  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(f(f(Y,Z),Y),f(Y,W)),Y) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(f(f(Y,Y),f(Z,Z)),f(W,Z)) )).
