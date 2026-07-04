% order5_0211  eq1=581 eq2=11672  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(Y,f(Z,f(Z,f(Z,Z)))) )).
fof(neg, negated_conjecture, ? [U,W,X,Y,Z] : ( X != f(Y,f(f(Z,f(W,W)),f(U,U))) )).
