% hard3_0335  eq1=3130 eq2=2119  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(f(f(Y,X),Z),Z),X) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(f(f(Y,X),Z),f(W,X)) )).
