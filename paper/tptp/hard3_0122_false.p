% hard3_0122  eq1=1009 eq2=130  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(Y,f(f(Z,W),f(W,X))) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(Y,f(f(Y,Z),X)) )).
