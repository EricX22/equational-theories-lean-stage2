% order5_0001  eq1=62264 eq2=17075  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( f(f(X,Y),Z) = f(f(f(X,W),Y),W) )).
fof(neg, negated_conjecture, ? [X,Y] : ( X != f(f(X,Y),f(Y,f(Y,f(Y,X)))) )).
