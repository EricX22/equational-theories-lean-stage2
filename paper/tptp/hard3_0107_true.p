% hard3_0107  eq1=859 eq2=2878  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(X,f(f(Y,Z),f(Y,W))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(f(X,f(Y,Y)),Z),X) )).
