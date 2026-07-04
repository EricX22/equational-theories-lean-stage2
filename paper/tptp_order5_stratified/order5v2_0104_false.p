% order5v2_0104  eq1=36794 eq2=22598  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(f(f(Y,Z),X),f(Y,Y)),Y) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(f(Y,f(Y,X)),f(f(X,Z),W)) )).
