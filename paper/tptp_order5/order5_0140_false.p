% order5_0140  eq1=30000 eq2=12570  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(Y,f(Z,f(W,f(X,Z)))),W) )).
fof(neg, negated_conjecture, ? [U,W,X,Y,Z] : ( X != f(Y,f(f(f(Z,W),U),f(W,Y))) )).
