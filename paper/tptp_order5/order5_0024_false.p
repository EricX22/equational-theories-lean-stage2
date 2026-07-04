% order5_0024  eq1=19202 eq2=9855  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(Y,Y),f(f(Z,Z),f(W,Y))) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(Y,f(f(Z,W),f(Y,f(Z,W)))) )).
