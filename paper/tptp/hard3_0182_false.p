% hard3_0182  eq1=1618 eq2=3093  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(Y,Z),f(W,f(W,X))) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(f(f(X,Y),Z),Z),X) )).
