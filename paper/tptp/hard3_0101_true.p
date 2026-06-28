% hard3_0101  eq1=796 eq2=2165  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(Y,f(Z,f(f(W,Y),X))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(f(Y,Z),X),f(Y,X)) )).
