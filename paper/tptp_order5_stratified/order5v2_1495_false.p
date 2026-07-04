% order5v2_1495  eq1=17799 eq2=52840  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(Y,Z),f(W,f(W,f(Z,Z)))) )).
fof(neg, negated_conjecture, ? [U,V,W,X,Y,Z] : ( f(X,Y) != f(f(f(Z,f(W,Y)),U),V) )).
